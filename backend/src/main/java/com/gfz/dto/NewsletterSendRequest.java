package com.gfz.dto;

import jakarta.validation.constraints.NotBlank;

public record NewsletterSendRequest(
    @NotBlank String sujet,
    @NotBlank String message
) {}
