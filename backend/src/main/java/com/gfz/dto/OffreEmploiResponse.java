package com.gfz.dto;

import java.time.LocalDate;

public record OffreEmploiResponse(
    Long id,
    String titre,
    String type,
    String localisation,
    String duree,
    LocalDate dateExpiration,
    String resume
) {}
