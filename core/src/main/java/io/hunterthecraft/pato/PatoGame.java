package io.hunterthecraft.pato;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;

public class PatoGame extends Game {
    public SpriteBatch batch;

    @Override
    public void create() {
        batch = new SpriteBatch();
        setScreen(new LoadingScreen(this));
    }

    @Override
    public void dispose() {
        batch.dispose();
    }
}