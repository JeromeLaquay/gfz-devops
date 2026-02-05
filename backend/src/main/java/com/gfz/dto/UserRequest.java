package com.gfz.dto;

import jakarta.validation.constraints.NotBlank;

public record UserRequest(
    @NotBlank String username,
    String email,
    String password,
    String name
) {}
