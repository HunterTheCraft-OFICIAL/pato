// core/src/main/java/io/hunterthecraft/pato/PatoGame.java
package io.hunterthecraft.pato;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import io.hunterthecraft.pato.screen.SplashScreen; // ← CORRIGIDO: SplashScreen

public class PatoGame extends Game {
    public SpriteBatch batch;

    @Override
    public void create() {
        batch = new SpriteBatch();
        setScreen(new SplashScreen(this)); // ← CORRIGIDO
    }

    @Override
    public void dispose() {
        batch.dispose();
    }
}