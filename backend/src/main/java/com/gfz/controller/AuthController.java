package com.gfz.controller;

import com.gfz.dto.ForgotPasswordRequest;
import com.gfz.dto.LoginRequest;
import com.gfz.dto.LoginResponse;
import com.gfz.mappingservice.UserMappingService;
import com.gfz.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "http://localhost:3000")
public class AuthController {
    private final AuthService authService;
    private final UserMappingService userMappingService;

    public AuthController(AuthService authService, UserMappingService userMappingService) {
        this.authService = authService;
        this.userMappingService = userMappingService;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest request) {
        try {
            LoginResponse response = authService.login(request);
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            Map<String, String> error = new HashMap<>();
            error.put("message", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("message", "Erreur lors de la connexion: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }

    @PostMapping("/forgot-password")
    public ResponseEntity<?> forgotPassword(@Valid @RequestBody ForgotPasswordRequest request) {
        try {
            userMappingService.demanderReinitialisationMotDePasse(request.emailOrUsername());
            Map<String, String> response = new HashMap<>();
            response.put("message", "Si un compte existe avec cet email/identifiant, un lien de réinitialisation a été envoyé.");
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            Map<String, String> error = new HashMap<>();
            error.put("message", "Si un compte existe avec cet email/identifiant, un lien de réinitialisation a été envoyé.");
            return ResponseEntity.ok(error);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("message", "Erreur lors de la demande de réinitialisation");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
        }
    }
}
