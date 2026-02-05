package com.gfz.controller;

import com.gfz.dto.OffreEmploiRequest;
import com.gfz.dto.OffreEmploiResponse;
import com.gfz.mappingservice.OffreEmploiMappingService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/offres-emploi")
@CrossOrigin(origins = "http://localhost:3000")
public class OffreEmploiController {
    private final OffreEmploiMappingService offreEmploiMappingService;

    public OffreEmploiController(OffreEmploiMappingService offreEmploiMappingService) {
        this.offreEmploiMappingService = offreEmploiMappingService;
    }

    @PostMapping
    public ResponseEntity<OffreEmploiResponse> create(@Valid @RequestBody OffreEmploiRequest request) {
        OffreEmploiResponse response = offreEmploiMappingService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<List<OffreEmploiResponse>> findAll() {
        List<OffreEmploiResponse> responses = offreEmploiMappingService.findAll();
        return ResponseEntity.ok(responses);
    }

    @GetMapping("/valides")
    public ResponseEntity<List<OffreEmploiResponse>> findValid() {
        List<OffreEmploiResponse> responses = offreEmploiMappingService.findValid();
        return ResponseEntity.ok(responses);
    }

    @GetMapping("/{id}")
    public ResponseEntity<OffreEmploiResponse> findById(@PathVariable Long id) {
        OffreEmploiResponse response = offreEmploiMappingService.findById(id);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/{id}")
    public ResponseEntity<OffreEmploiResponse> update(@PathVariable Long id, 
                                                      @Valid @RequestBody OffreEmploiRequest request) {
        OffreEmploiResponse response = offreEmploiMappingService.update(id, request);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        offreEmploiMappingService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
