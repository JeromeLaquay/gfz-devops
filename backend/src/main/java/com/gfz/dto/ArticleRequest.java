package com.gfz.dto;

import jakarta.validation.constraints.NotBlank;
import java.time.LocalDateTime;
public record ArticleRequest(
    @NotBlank String titre,
    String image,
    String contenu,
    LocalDateTime dateCreation
) {}
