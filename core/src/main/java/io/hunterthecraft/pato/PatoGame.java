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
        font.getData().setScale(2.5f); // maior para mobile
    }

    @Override
    public void render() {
        ScreenUtils.clear(0, 0, 0.2f, 1); // fundo azul escuro

        batch.begin();

        // ✅ Usa back buffer (sempre atualizado, mesmo na primeira render)
        int w = Gdx.graphics.getBackBufferWidth();
        int h = Gdx.graphics.getBackBufferHeight();

        // Centraliza o texto
        float x = w / 2f - font.getBounds("PATO FUNCIONANDO!").width / 2;
        float y = h / 2f + font.getBounds("PATO FUNCIONANDO!").height / 2;

        font.draw(batch, "PATO FUNCIONANDO!", x, y);

        batch.end();
    }

    @Override
    public void dispose() {
        batch.dispose();
        font.dispose();
    }
}