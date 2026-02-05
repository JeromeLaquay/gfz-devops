package com.gfz.controller;

import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.MalformedURLException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/documents")
@CrossOrigin(origins = "http://localhost:3000")
public class DocumentController {
    private final Path documentsPath;

    public DocumentController() {
        this.documentsPath = determineDocumentsPath();
        initDocumentsDirectory();
    }

    private Path determineDocumentsPath() {
        String documentsDir = System.getenv("DOCUMENTS_DIR");
        if (documentsDir != null && !documentsDir.isEmpty()) {
            return Paths.get(documentsDir);
        }
        
        String userDir = System.getProperty("user.dir");
        Path projectRoot = Paths.get(userDir);
        
        if (projectRoot.toString().equals("/app")) {
            return Paths.get("/app/documents");
        }
        
        if (projectRoot.endsWith("backend")) {
            return projectRoot.resolve("src/main/resources/documents");
        }
        
        return projectRoot.resolve("backend/src/main/resources/documents");
    }

    private void initDocumentsDirectory() {
        try {
            if (!Files.exists(documentsPath)) {
                Files.createDirectories(documentsPath);
            }
            System.out.println("Documents directory: " 
                + documentsPath.toAbsolutePath());
        } catch (IOException e) {
            throw new RuntimeException(
                "Impossible de créer le dossier documents: " 
                + documentsPath.toAbsolutePath(), e);
        }
    }

    @PostMapping("/upload")
    public ResponseEntity<Map<String, String>> uploadDocument(
            @RequestParam("file") MultipartFile file) {
        try {
            validateFile(file);
            return ResponseEntity.ok(saveFile(file));
        } catch (IllegalArgumentException e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", e.getMessage());
            return ResponseEntity.badRequest().body(error);
        } catch (Exception e) {
            System.err.println("Erreur upload: " + e.getMessage());
            e.printStackTrace();
            Map<String, String> error = new HashMap<>();
            error.put("error", "Erreur lors de l'upload du fichier: " 
                + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(error);
        }
    }

    private void validateFile(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new IllegalArgumentException("Aucun fichier fourni");
        }
        
        String filename = file.getOriginalFilename();
        if (filename == null || filename.isEmpty()) {
            throw new IllegalArgumentException("Nom de fichier invalide");
        }
        
        String extension = getExtension(filename).toLowerCase();
        List<String> allowedExtensions = List.of(
            "pdf", "doc", "docx", "xls", "xlsx", "txt"
        );
        
        if (!allowedExtensions.contains(extension)) {
            throw new IllegalArgumentException(
                "Format non autorisé. Formats acceptés: " 
                + String.join(", ", allowedExtensions)
            );
        }
        
        long maxSize = 50 * 1024 * 1024; // 50 MB
        if (file.getSize() > maxSize) {
            throw new IllegalArgumentException(
                "Fichier trop volumineux (max 50 MB)"
            );
        }
    }

    private Map<String, String> saveFile(MultipartFile file) 
            throws IOException {
        String originalFilename = file.getOriginalFilename();
        String filename = sanitizeFilename(originalFilename);
        Path targetPath = documentsPath.resolve(filename);

        Files.copy(file.getInputStream(), targetPath, 
            StandardCopyOption.REPLACE_EXISTING);

        Map<String, String> response = new HashMap<>();
        response.put("filename", filename);
        response.put("url", "/documents/" + filename);
        response.put("message", "Document téléchargé avec succès");
        return response;
    }
    
    private String getExtension(String filename) {
        int lastDot = filename.lastIndexOf('.');
        if (lastDot == -1 || lastDot == filename.length() - 1) {
            return "";
        }
        return filename.substring(lastDot + 1);
    }

    @GetMapping
    public ResponseEntity<List<Map<String, Object>>> listDocuments() {
        try {
            List<Map<String, Object>> documents = Files.list(documentsPath)
                .filter(Files::isRegularFile)
                .map(this::fileToMap)
                .collect(Collectors.toList());
            return ResponseEntity.ok(documents);
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(List.of());
        }
    }

    private Map<String, Object> fileToMap(Path path) {
        Map<String, Object> fileInfo = new HashMap<>();
        String filename = path.getFileName().toString();
        fileInfo.put("filename", filename);
        fileInfo.put("url", "/documents/" + filename);
        try {
            fileInfo.put("size", Files.size(path));
        } catch (IOException e) {
            fileInfo.put("size", 0);
        }
        return fileInfo;
    }

    @GetMapping("/{filename:.+}")
    public ResponseEntity<Resource> downloadDocument(
            @PathVariable String filename) {
        try {
            return buildResourceResponse(filename);
        } catch (MalformedURLException e) {
            return ResponseEntity.notFound().build();
        }
    }

    private ResponseEntity<Resource> buildResourceResponse(String filename) 
            throws MalformedURLException {
        Path filePath = documentsPath.resolve(filename);
        Resource resource = new UrlResource(filePath.toUri());

        if (!resource.exists()) {
            return ResponseEntity.notFound().build();
        }

        String contentType = determineContentType(filename);
        
        return ResponseEntity.ok()
            .contentType(MediaType.parseMediaType(contentType))
            .header(HttpHeaders.CONTENT_DISPOSITION, 
                "inline; filename=\"" + filename + "\"")
            .body(resource);
    }

    @DeleteMapping("/{filename:.+}")
    public ResponseEntity<Map<String, String>> deleteDocument(
            @PathVariable String filename) {
        try {
            Path filePath = documentsPath.resolve(filename);
            Files.deleteIfExists(filePath);
            
            Map<String, String> response = new HashMap<>();
            response.put("message", "Document supprimé avec succès");
            return ResponseEntity.ok(response);
        } catch (IOException e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Erreur lors de la suppression");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(error);
        }
    }

    private String sanitizeFilename(String filename) {
        return filename.replaceAll("[^a-zA-Z0-9._-]", "_");
    }

    private String determineContentType(String filename) {
        String extension = filename.substring(filename.lastIndexOf(".") + 1)
            .toLowerCase();
        
        return switch (extension) {
            case "pdf" -> "application/pdf";
            case "doc" -> "application/msword";
            case "docx" -> "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
            case "xls" -> "application/vnd.ms-excel";
            case "xlsx" -> "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
            case "txt" -> "text/plain";
            default -> "application/octet-stream";
        };
    }
}
