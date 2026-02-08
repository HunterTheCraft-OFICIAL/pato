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
        font = new BitmapFont(); // usa fonte embutida do LibGDX
        font.setColor(Color.WHITE);
        font.getData().setScale(2.0f); // aumenta o tamanho
    }

    @Override
    public void render() {
        ScreenUtils.clear(0, 0, 0.2f, 1); // fundo azul escuro
        
        batch.begin();
        // Posição segura: centro da tela
        float x = Gdx.graphics.getWidth() / 2f;
        float y = Gdx.graphics.getHeight() / 2f;
        font.draw(batch, "PATO VIVO!", x, y);
        batch.end();
    }

    @Override
    public void dispose() {
        batch.dispose();
        font.dispose();
    }
}