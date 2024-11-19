package org.example;

import io.javalin.Javalin;
import org.example.stream.POSTBody;
import org.example.stream.POSTReturn;


public class App {
    public static void main(String[] args) {
        Javalin app = Javalin.create().start(7000);
        app.get("/", ctx -> ctx.result("Hello, Javalin!"));

        app.post("/stream", ctx -> {
            POSTBody requestBody = ctx.bodyAsClass(POSTBody.class);
            int i = 0;
            for (int j = 0; j < 1000000; j++) {
                i += 1;
            }

            double timestamp = requestBody.getTimestamp();
            float output = requestBody.getData().get("x") + requestBody.getData().get("y");
            POSTReturn postReturn = new POSTReturn(output, System.currentTimeMillis() / 1000.0,
                    System.currentTimeMillis() / 1000.0 - timestamp);

            ctx.json(postReturn);

        });
    }
}