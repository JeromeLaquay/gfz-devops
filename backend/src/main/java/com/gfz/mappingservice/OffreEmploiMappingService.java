package com.gfz.mappingservice;

import com.gfz.dto.OffreEmploiRequest;
import com.gfz.dto.OffreEmploiResponse;
import com.gfz.entity.OffreEmploi;
import com.gfz.mapper.OffreEmploiMapper;
import com.gfz.service.OffreEmploiService;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class OffreEmploiMappingService {
    private final OffreEmploiMapper offreEmploiMapper;
    private final OffreEmploiService offreEmploiService;

    public OffreEmploiMappingService(OffreEmploiMapper offreEmploiMapper, 
                                     OffreEmploiService offreEmploiService) {
        this.offreEmploiMapper = offreEmploiMapper;
        this.offreEmploiService = offreEmploiService;
    }

    public OffreEmploiResponse create(OffreEmploiRequest request) {
        OffreEmploi offre = offreEmploiMapper.toEntity(request);
        OffreEmploi saved = offreEmploiService.save(offre);
        return offreEmploiMapper.toResponse(saved);
    }

    public List<OffreEmploiResponse> findAll() {
        List<OffreEmploi> offres = offreEmploiService.findAll();
        return offres.stream()
            .map(offreEmploiMapper::toResponse)
            .collect(Collectors.toList());
    }

    public List<OffreEmploiResponse> findValid() {
        List<OffreEmploi> offres = offreEmploiService.findValid();
        return offres.stream()
            .map(offreEmploiMapper::toResponse)
            .collect(Collectors.toList());
    }

    public OffreEmploiResponse findById(Long id) {
        OffreEmploi offre = offreEmploiService.findById(id);
        return offreEmploiMapper.toResponse(offre);
    }

    public OffreEmploiResponse update(Long id, OffreEmploiRequest request) {
        OffreEmploi offre = offreEmploiMapper.toEntity(request);
        OffreEmploi updated = offreEmploiService.update(id, offre);
        return offreEmploiMapper.toResponse(updated);
    }

    public void delete(Long id) {
        offreEmploiService.delete(id);
    }
}
