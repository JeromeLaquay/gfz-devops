package com.gfz.service;

import com.gfz.entity.OffreEmploi;
import com.gfz.repository.OffreEmploiRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class OffreEmploiService {
    private final OffreEmploiRepository repository;

    public OffreEmploiService(OffreEmploiRepository repository) {
        this.repository = repository;
    }

    public OffreEmploi save(OffreEmploi offre) {
        return repository.save(offre);
    }

    public List<OffreEmploi> findAll() {
        return repository.findAll();
    }

    public List<OffreEmploi> findValid() {
        return repository.findByDateExpirationAfter(LocalDate.now());
    }

    public OffreEmploi findById(Long id) {
        OffreEmploi offre = repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Offre non trouvée"));
        return offre;
    }

    public OffreEmploi update(Long id, OffreEmploi offre) {
        OffreEmploi existingOffre = repository.findById(id)
            .orElseThrow(() -> new RuntimeException("Offre non trouvée"));
        updateOffre(offre, existingOffre);
        OffreEmploi saved = repository.save(existingOffre);
        return saved;
    }

    private void updateOffre(OffreEmploi offre, OffreEmploi existingOffre) {
        existingOffre.setTitre(offre.getTitre());
        existingOffre.setType(offre.getType());
        existingOffre.setLocalisation(offre.getLocalisation());
        existingOffre.setDuree(offre.getDuree());
        existingOffre.setDateExpiration(offre.getDateExpiration());
        existingOffre.setResume(offre.getResume());
    }

    public void delete(Long id) {
        repository.deleteById(id);
    }
}
