package org.example;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class FeaturesExtractor {
    private List<String> countries;
    private List<String> currencies;

    public FeaturesExtractor() throws IOException {
        loadCountriesFromFile();
        loadCurrenciesFromFile();
    }

    public static int countWords(Article article) {
        return article.getBody().size();
    }

    public static int countUppercaseWords(Article article) {
        int counter = 0;
        for (String word : article.getBody()) {
            if (word.matches("[A-Z]+")) {
                //System.out.println(word);
                counter++;
            }
        }
        return counter;
    }

    public int countWordsStartWithUppercase(Article article) {
        int counter = 0;
        for (String word : article.getBody()) {
            if (word.matches("[A-Z].*")) {
                //System.out.println(word);
                counter++;
            }
        }
        return counter;
    }

    public String findFirsCountry(Article article) {
        int numOfWords = article.getBody().size();

        for (int i = 0; i < numOfWords; i++) {
            for (int j = i + 1; j <= numOfWords; j++) {
                if (j > i + 3) {
                    break;
                }
                String maybeCountry = String.join(" ", article.getBody().subList(i, j));
                if (this.countries.contains(maybeCountry)) {
                    //System.out.println(maybeCountry);
                    return standardNameCountry(maybeCountry);
                }
            }
        }
        return null;

//        for (String word : article.getBody()) {
//            if (this.countries.contains(word)) {
//                //System.out.println(word);
//                return word;
//            }
//        }
//        return null;
    }

    public int countUniqueCountries(Article article) {
        List<String> uniqueCountries = new ArrayList<>();
        //int counter = 0;
        int numOfWords = article.getBody().size();

        for (int i = 0; i < numOfWords; i++) {
            for (int j = i + 1; j <= numOfWords; j++) {
                if (j > i + 3) {
                    break;
                }
                String maybeCountry = String.join(" ", article.getBody().subList(i, j));
                if (this.countries.contains(maybeCountry)) {
                    //System.out.println(standardNameCountry(maybeCountry));
                    if (!uniqueCountries.contains(standardNameCountry(maybeCountry))) {
                        uniqueCountries.add(standardNameCountry(maybeCountry));
                    }
                    //counter++;
                    i = j - 1;
                    break;
                }
            }
        }
        return uniqueCountries.size();
//        int counter = 0;
//        for (String word : article.getBody()) {
//            if (this.countries.contains(word)) {
//                System.out.println(word);
//                counter++;
//            }
//        }
//        return counter;
    }

    public String findMostCommonCountry(Article article) {
        List<String> country = new ArrayList<>();
        List<Integer> counts = new ArrayList<>();

        int numOfWords = article.getBody().size();

        for (int i = 0; i < numOfWords; i++) {
            for (int j = i + 1; j <= numOfWords; j++) {
                if (j > i + 3) {
                    break;
                }

                String maybeCountry = String.join(" ", article.getBody().subList(i, j));

                if (this.countries.contains(maybeCountry)) {
                    int index = country.indexOf(standardNameCountry(maybeCountry));
                    if (index != -1) {
                        counts.set(index, counts.get(index) + 1);
                    } else {
                        country.add(standardNameCountry(maybeCountry));
                        counts.add(1);
                    }
                    i = j - 1;
                    break;
                }
            }
        }
        if (country.isEmpty()) {
            return null;
        }

        int maxValue = 0;
        int foundIndex = 0;
        for (int i = 0; i < counts.size(); i++) {
            if (counts.get(i) > maxValue) {
                maxValue = counts.get(i);
                foundIndex = i;
            }
        }
        return country.get(foundIndex);
    }

    public String findFirsCurrency(Article article) {
        for (String word : article.getBody()) {
            if (this.currencies.contains(word.toLowerCase())) {
                //System.out.println(word);
                return standardNameCurrencies(word.toLowerCase());
            }
        }
        return null;
    }

    public int countCountriesAndCurrencies(Article article) {
        int counter = 0;

        for (String word : article.getBody()) {
            if (this.currencies.contains(word.toLowerCase())) {
                //System.out.println(word);
                counter++;
            }
        }

        int numOfWords = article.getBody().size();
        for (int i = 0; i < numOfWords; i++) {
            for (int j = i + 1; j <= numOfWords; j++) {
                if (j > i + 3) {
                    break;
                }
                String maybeCountry = String.join(" ", article.getBody().subList(i, j));
                if (this.countries.contains(maybeCountry)) {
                    //System.out.println(maybeCountry);
                    counter++;
                    i = j - 1;
                    break;
                }
            }
        }

        return counter;
    }

    private void loadCountriesFromFile() throws IOException {
        this.countries = new ArrayList<>();
        try {
            countries = Files.readAllLines(Paths.get("src/main/resources/keyWords/countries.txt"));
        } catch (IOException e) {
            throw new IOException();
        }
    }

    private void loadCurrenciesFromFile() throws IOException {
        this.currencies = new ArrayList<>();
        try {
            currencies = Files.readAllLines(Paths.get("src/main/resources/keyWords/currencies.txt"));
        } catch (IOException e) {
            throw new IOException();
        }
    }

    private String standardNameCountry(String country) {
        if (country == null) {
            return null;
        }

        if (country.equalsIgnoreCase("USA") || country.equalsIgnoreCase("United States") || country.equalsIgnoreCase("US")) {
            return "USA";
        } else if (country.equalsIgnoreCase("UK") || country.equalsIgnoreCase("United Kingdom")) {
            return "UK";
        } else if (country.equalsIgnoreCase("West Germany") || country.equalsIgnoreCase("Germany")) {
            return "West Germany";
        }
        return country;
    }

    private String standardNameCurrencies(String currency) {
        if (currency == null) {
            return null;
        }

        if (currency.equalsIgnoreCase("dollar") || currency.equalsIgnoreCase("dollars") || currency.equalsIgnoreCase("dlr")
                || currency.equalsIgnoreCase("dlrs")) {
            return "dollar";
        } else if (currency.equalsIgnoreCase("mark") || currency.equalsIgnoreCase("marks") ||
                currency.equalsIgnoreCase("dmk") || currency.equalsIgnoreCase("dmks")) {
            return "mark";
        } else if (currency.equalsIgnoreCase("yens") || currency.equalsIgnoreCase("yen")) {
            return "yen";
        } else if (currency.equalsIgnoreCase("can") || currency.equalsIgnoreCase("cans")) {
            return "can";
        } else if (currency.equalsIgnoreCase("franc") || currency.equalsIgnoreCase("francs")
                || currency.equalsIgnoreCase("ffr") || currency.equalsIgnoreCase("ffrs")) {
            return "franc";
        } else if (currency.equalsIgnoreCase("sterling") || currency.equalsIgnoreCase("sterlings")
                || currency.equalsIgnoreCase("stg") || currency.equalsIgnoreCase("stgs")) {
            return "stg";
        }
        return currency;
    }
}
