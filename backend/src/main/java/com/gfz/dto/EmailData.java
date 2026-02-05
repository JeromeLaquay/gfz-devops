package com.gfz.dto;

public record EmailData(
    String from,
    String destinataire,
    String nomDestinataire,
    String sujetOriginal,
    String messageReponse
) {}
