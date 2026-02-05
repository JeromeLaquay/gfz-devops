package com.gfz.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public record ContactRequest(
    @NotBlank String nom,
    @Email @NotBlank String email,
    String sujet,
    @NotBlank String message,
    boolean reply
) {}
