package com.gfz.service;

import com.gfz.dto.EmailData;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
public class EmailService {
    private final JavaMailSender mailSender;
    
    @Value("${spring.mail.username}")
    private String fromEmail;
    
    @Value("${app.email.from-name:GFZ Online}")
    private String fromName;

    public EmailService(JavaMailSender mailSender) {
        this.mailSender = mailSender;
    }

    public void envoyerEmail(EmailData emailData) {
        SimpleMailMessage email = new SimpleMailMessage();
        email.setFrom(emailData.from());
        email.setTo(emailData.destinataire());
        email.setSubject(emailData.sujetOriginal());
        email.setText(emailData.messageReponse());
        mailSender.send(email);
    }

    public void envoyerReponse(EmailData emailData) {
        SimpleMailMessage email = new SimpleMailMessage();
        email.setFrom(fromEmail);
        email.setTo(emailData.destinataire());
        email.setSubject(construireSujet(emailData.sujetOriginal()));
        email.setText(construireCorps(emailData));
        mailSender.send(email);
    }

    private String construireSujet(String sujetOriginal) {
        return "Re: " + (sujetOriginal != null ? sujetOriginal : "Votre message");
    }

    private String construireCorps(EmailData emailData) {
        String corps = "Bonjour " + emailData.nomDestinataire() + ",\n\n";
        corps += emailData.messageReponse() + "\n\n";
        corps += "Cordialement,\n";
        corps += "L'équipe " + fromName;
        return corps;
    }
}
