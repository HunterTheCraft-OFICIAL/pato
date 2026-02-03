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
        Thread.setDefaultUncaughtExceptionHandler((thread, throwable) -> {
            Gdx.app.error("CRASH", "Unhandled exception", throwable);
            String message = throwable.toString() + "\n" + getStackTrace(throwable);
            setScreen(new ErrorScreen(PatoGame.this, message));
        });

        batch = new SpriteBatch();
        try {
            setScreen(new SplashScreen(this));
        } catch (Exception e) {
            Gdx.app.error("STARTUP", "Failed to start", e);
            setScreen(new ErrorScreen(this, e.toString()));
        }
    }

    private String getStackTrace(Throwable t) {
        StringBuilder sb = new StringBuilder();
        for (StackTraceElement element : t.getStackTrace()) {
            sb.append(element.toString()).append("\n");
        }
        return sb.toString();
    }

    @Override
    public void dispose() {
        batch.dispose();
    }
}