package com.gfz.controller;

import com.gfz.dto.ArticleRequest;
import com.gfz.dto.ArticleResponse;
import com.gfz.mappingservice.ArticleMappingService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/articles")
@CrossOrigin(origins = "http://localhost:3000")
public class ArticleController {
    private final ArticleMappingService articleMappingService;

    public ArticleController(ArticleMappingService articleMappingService) {
        this.articleMappingService = articleMappingService;
    }

    @PostMapping
    public ResponseEntity<ArticleResponse> create(@Valid @RequestBody ArticleRequest request) {
        try {
            ArticleResponse response = articleMappingService.create(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(response);
        } catch (Exception e) {
            System.err.println("Erreur lors de la création de l'article: " + e.getMessage());
            e.printStackTrace();
            throw e;
        }
    }

    @GetMapping
    public ResponseEntity<List<ArticleResponse>> findAll() {
        List<ArticleResponse> responses = articleMappingService.findAll();
        return ResponseEntity.ok(responses);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ArticleResponse> findById(@PathVariable Long id) {
        ArticleResponse response = articleMappingService.findById(id);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/{id}")
    public ResponseEntity<ArticleResponse> update(@PathVariable Long id, 
                                                  @Valid @RequestBody ArticleRequest request) {
        ArticleResponse response = articleMappingService.update(id, request);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        articleMappingService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
