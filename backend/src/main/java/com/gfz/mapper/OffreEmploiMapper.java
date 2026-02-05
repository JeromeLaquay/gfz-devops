package com.gfz.mapper;

import com.gfz.dto.OffreEmploiRequest;
import com.gfz.dto.OffreEmploiResponse;
import com.gfz.entity.OffreEmploi;
import org.springframework.stereotype.Component;

@Component
public class OffreEmploiMapper {
    public OffreEmploi toEntity(OffreEmploiRequest request) {
        OffreEmploi offre = new OffreEmploi();
        offre.setTitre(request.titre());
        offre.setType(request.type());
        offre.setLocalisation(request.localisation());
        offre.setDuree(request.duree());
        offre.setDateExpiration(request.dateExpiration());
        offre.setResume(request.resume());
        return offre;
    }

    public OffreEmploiResponse toResponse(OffreEmploi offre) {
        return new OffreEmploiResponse(
            offre.getId(),
            offre.getTitre(),
            offre.getType(),
            offre.getLocalisation(),
            offre.getDuree(),
            offre.getDateExpiration(),
            offre.getResume()
        );
    }
}
