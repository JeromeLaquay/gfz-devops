package com.gfz.dto;

import java.time.LocalDateTime;

public record ArticleResponse(
    Long id,
    String titre,
    String image,
    String contenu,
    LocalDateTime dateCreation
) {}
