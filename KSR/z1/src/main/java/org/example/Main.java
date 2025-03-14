package org.example;

import org.jsoup.nodes.Document;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) throws IOException {
        //Document doc = new Document("C:\\Users\\Julia\\Downloads\\reuters+21578+text+categorization+collection\\reuters21578\\reut2-021.sgm");
        //List<String>
        Reader r = new Reader("src/main/resources");
        int count = 0;
        for (Article a : r.read()) {
           System.out.println(a.getCountry() + "\n" + a.getBody());
            count ++;
        }
        System.out.println(count);
        //System.out.println(r.read().get(0).getCountry() + "\n" + r.read().get(0).getBody());
//        r.read("reut2-002.sgm");
    }
}