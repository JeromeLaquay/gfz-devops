package com.gfz.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public record NewsletterRequest(
    @NotBlank String name,
    @Email @NotBlank String email
) {}
