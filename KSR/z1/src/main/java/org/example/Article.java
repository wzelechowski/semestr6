package org.example;

import java.util.Arrays;
import java.util.List;

public class Article {
    private final List<String> body;
    private final String place;

    public Article(String body, String country) {
        this.body = Arrays.asList(body.replaceAll("[^a-zA-Z ]", "").trim().split("\\s+"));
        this.place = country;
    }

    public String getCountry() {
        return place;
    }

    public List<String> getBody() {
        return body;
    }

}

