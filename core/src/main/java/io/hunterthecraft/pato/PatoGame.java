// core/src/io/hunterthecraft/pato/PatoGame.java
package io.hunterthecraft.pato;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import io.hunterthecraft.pato.screen.BugCenterScreen;
import io.hunterthecraft.pato.screen.StartupScreen;

public class PatoGame extends Game {

    @Override
    public void create() {
        // Handler global de erros: captura qualquer exceção não tratada
        Thread.setDefaultUncaughtExceptionHandler((thread, throwable) -> {
            Gdx.app.error("CRASH", "Erro não tratado", throwable);
            String log = throwable.toString() + "\n" + getStackTrace(throwable);
            setScreen(new BugCenterScreen(PatoGame.this, log));
        });

        // Inicia com a tela de startup (não depende de assets externos)
        try {
            setScreen(new StartupScreen(this));
        } catch (Exception e) {
            Gdx.app.error("PatoGame", "Falha crítica na inicialização", e);
            setScreen(new BugCenterScreen(this, e.toString()));
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
        // Nada a descartar aqui — cada tela gerencia seus próprios recursos
    }
}