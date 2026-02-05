package com.gfz.controller;

import com.gfz.dto.NewsletterRequest;
import com.gfz.dto.NewsletterSendRequest;
import com.gfz.service.NewsletterService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/newsletter")
@CrossOrigin(origins = "http://localhost:3000")
public class NewsletterController {
    private final NewsletterService newsletterService;

    public NewsletterController(NewsletterService newsletterService) {
        this.newsletterService = newsletterService;
    }

    @PostMapping("/subscribe")
    public ResponseEntity<String> subscribe(@Valid @RequestBody NewsletterRequest request) {
        newsletterService.subscribe(request);
        return ResponseEntity.ok("Inscription réussie");
    }

    @PostMapping("/unsubscribe")
    public ResponseEntity<String> unsubscribe(@RequestParam String email) {
        newsletterService.unsubscribe(email);
        return ResponseEntity.ok("Désinscription réussie");
    }

    @PostMapping("/send")
    public ResponseEntity<String> send(@Valid @RequestBody NewsletterSendRequest request) {
        newsletterService.envoyerNewsletter(request);
        return ResponseEntity.ok("Newsletter envoyée avec succès");
    }
}
