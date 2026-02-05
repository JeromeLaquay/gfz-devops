package com.gfz.dto;

import java.time.LocalDateTime;

public record ContactResponse(
    Long id,
    String nom,
    String email,
    String sujet,
    String message,
    LocalDateTime dateCreation
) {}
