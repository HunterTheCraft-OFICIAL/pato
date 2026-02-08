// core/src/io/hunterthecraft/pato/PatoGame.java
package io.hunterthecraft.pato;

import com.badlogic.gdx.Game;
import io.hunterthecraft.pato.screen.StartupScreen;

public class PatoGame extends Game {
    @Override
    public void create() {
        // Vai direto para a tela de startup
        setScreen(new StartupScreen(this));
    }
}