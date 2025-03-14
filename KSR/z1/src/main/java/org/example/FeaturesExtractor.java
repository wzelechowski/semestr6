package org.example;

public class FeaturesExtractor {
    private FeaturesExtractor() {}

    public static int countWords(Article article) {
        return article.getBody().size();
    }

}
