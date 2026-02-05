package com.gfz.mapper;

import com.gfz.dto.ArticleRequest;
import com.gfz.dto.ArticleResponse;
import com.gfz.entity.Article;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class ArticleMapper {
    public Article toEntity(ArticleRequest request) {
        Article article = new Article();
        article.setTitre(request.titre());
        article.setImage(request.image());
        article.setContenu(request.contenu());
        LocalDateTime dateCreation = request.dateCreation() != null 
            ? request.dateCreation() 
            : LocalDateTime.now();
        article.setDateCreation(dateCreation);
        return article;
    }

    public ArticleResponse toResponse(Article article) {
        return new ArticleResponse(
            article.getId(),
            article.getTitre(),
            article.getImage(),
            article.getContenu(),
            article.getDateCreation()
        );
    }
}
