package com.gfz.mapper;

import com.gfz.dto.ContactRequest;
import com.gfz.dto.ContactResponse;
import com.gfz.entity.Contact;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class ContactMapper {
    public Contact toEntity(ContactRequest request) {
        Contact contact = new Contact();
        contact.setNom(request.nom());
        contact.setEmail(request.email());
        contact.setSujet(request.sujet());
        contact.setMessage(request.message());
        contact.setDateCreation(LocalDateTime.now());
        return contact;
    }

    public ContactResponse toResponse(Contact contact) {
        return new ContactResponse(
            contact.getId(),
            contact.getNom(),
            contact.getEmail(),
            contact.getSujet(),
            contact.getMessage(),
            contact.getDateCreation()
        );
    }
}
