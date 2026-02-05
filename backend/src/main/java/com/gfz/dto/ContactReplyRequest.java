package com.gfz.dto;

import jakarta.validation.constraints.NotBlank;

public record ContactReplyRequest(
    @NotBlank String message
) {}
