package com.gfz.controller;

import com.gfz.dto.ContactRequest;
import com.gfz.dto.ContactReplyRequest;
import com.gfz.dto.ContactResponse;
import com.gfz.mappingservice.ContactMappingService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/contact")
@CrossOrigin(origins = "http://localhost:3000")
public class ContactController {
    private final ContactMappingService contactMappingService;

    public ContactController(ContactMappingService contactMappingService) {
        this.contactMappingService = contactMappingService;
    }

    @PostMapping
    public ResponseEntity<ContactResponse> create(@Valid @RequestBody ContactRequest request) {
        ContactResponse response = contactMappingService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<List<ContactResponse>> findAll() {
        List<ContactResponse> responses = contactMappingService.findAll();
        return ResponseEntity.ok(responses);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ContactResponse> findById(@PathVariable Long id) {
        ContactResponse response = contactMappingService.findById(id);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        contactMappingService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{id}/reply")
    public ResponseEntity<String> reply(@PathVariable Long id, 
                                        @Valid @RequestBody ContactReplyRequest request) {
        contactMappingService.repondre(id, request.message());
        return ResponseEntity.ok("Réponse envoyée avec succès");
    }
}
