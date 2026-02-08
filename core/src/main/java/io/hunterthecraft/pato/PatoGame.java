// core/src/io/hunterthecraft/pato/PatoGame.java
package io.hunterthecraft.pato;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;

public class PatoGame extends Game {
    private SpriteBatch batch;
    private BitmapFont font;

    @Override
    public void create() {
        batch = new SpriteBatch();
        font = new BitmapFont();
        font.setColor(Color.WHITE);
    }

    @Override
    public void render() {
        ScreenUtils.clear(0, 0, 0.2f, 1); // fundo azul escuro
        
        batch.begin();
        font.draw(batch, "PATO FUNCIONANDO!", 100, Gdx.graphics.getHeight() - 100);
        batch.end();
    }

    @Override
    public void dispose() {
        batch.dispose();
        font.dispose();
    }
}