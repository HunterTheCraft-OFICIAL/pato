// core/src/io/hunterthecraft/pato/PatoGame.java
package io.hunterthecraft.pato;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import io.hunterthecraft.pato.screen.SplashScreen;
import io.hunterthecraft.pato.screen.ErrorScreen;

public class PatoGame extends Game {
    public SpriteBatch batch;

    @Override
    public void create() {
        // Handler global de erros
        Thread.setDefaultUncaughtExceptionHandler((thread, throwable) -> {
            Gdx.app.error("CRASH", "Unhandled exception", throwable);
            String message = throwable.toString();
            setScreen(new ErrorScreen(PatoGame.this, message));
        });

        batch = new SpriteBatch();
        Gdx.app.log("PatoGame", "Iniciando SplashScreen...");
        try {
            setScreen(new SplashScreen(this));
        } catch (Exception e) {
            Gdx.app.error("PatoGame", "Falha ao iniciar SplashScreen", e);
            setScreen(new ErrorScreen(this, e.toString()));
        }
    }

    @Override
    public void dispose() {
        batch.dispose();
    }
}