// core/src/io/hunterthecraft/pato/PatoGame.java
package io.hunterthecraft.pato;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import io.hunterthecraft.pato.screen.BugCenterScreen;
import io.hunterthecraft.pato.screen.StartupScreen;

public class PatoGame extends Game {

    @Override
    public void create() {
        Thread.setDefaultUncaughtExceptionHandler((thread, throwable) -> {
            Gdx.app.error("CRASH", "Erro não tratado", throwable);
            String log = throwable.toString();
            setScreen(new BugCenterScreen(PatoGame.this, log));
        });

        try {
            setScreen(new StartupScreen(this));
        } catch (Exception e) {
            Gdx.app.error("PatoGame", "Falha na inicialização", e);
            setScreen(new BugCenterScreen(this, e.toString()));
        }
    }

    @Override
    public void dispose() {}
}