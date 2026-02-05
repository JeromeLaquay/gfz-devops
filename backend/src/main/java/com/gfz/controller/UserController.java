package com.gfz.controller;

import com.gfz.dto.SetPasswordRequest;
import com.gfz.dto.UserDto;
import com.gfz.dto.UserRequest;
import com.gfz.mappingservice.UserMappingService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
@CrossOrigin(origins = "http://localhost:3000")
public class UserController {
    private final UserMappingService userMappingService;

    public UserController(UserMappingService userMappingService) {
        this.userMappingService = userMappingService;
    }

    @PostMapping
    public ResponseEntity<UserDto> create(@Valid @RequestBody UserRequest request) {
        UserDto response = userMappingService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<List<UserDto>> findAll() {
        List<UserDto> responses = userMappingService.findAll();
        return ResponseEntity.ok(responses);
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> findById(@PathVariable Long id) {
        UserDto response = userMappingService.findById(id);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        userMappingService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/set-password")
    public ResponseEntity<String> setPassword(@Valid @RequestBody SetPasswordRequest request) {
        userMappingService.definirMotDePasse(request.token(), request.password());
        return ResponseEntity.ok("Mot de passe défini avec succès");
    }
}
