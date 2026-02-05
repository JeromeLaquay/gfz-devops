package com.gfz.dto;

import jakarta.validation.constraints.NotBlank;
import java.time.LocalDate;

public record OffreEmploiRequest(
    @NotBlank String titre,
    String type,
    String localisation,
    String duree,
    LocalDate dateExpiration,
    String resume
) {}
