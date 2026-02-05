package com.gfz.dto;

import jakarta.validation.constraints.NotBlank;

public record SetPasswordRequest(
    @NotBlank String token,
    @NotBlank String password
) {}
