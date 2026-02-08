// core/src/io/hunterthecraft/pato/PatoGame.java
package io.hunterthecraft.pato;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.GlyphLayout;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;

public class PatoGame extends Game {
    private SpriteBatch batch;
    private BitmapFont font;
    private GlyphLayout layout;

    @Override
    public void create() {
        batch = new SpriteBatch();
        font = new BitmapFont();
        font.setColor(Color.WHITE);
        font.getData().setScale(2.5f);
        layout = new GlyphLayout();
    }

    @Override
    public void render() {
        ScreenUtils.clear(0, 0, 0.2f, 1);

        String text = "PATO FUNCIONANDO!";
        layout.setText(font, text);

        int w = Gdx.graphics.getBackBufferWidth();
        int h = Gdx.graphics.getBackBufferHeight();

        float x = w / 2f - layout.width / 2f;
        float y = h / 2f + layout.height / 2f;

        batch.begin();
        font.draw(batch, layout, x, y);
        batch.end();
    }

    @Override
    public void dispose() {
        if (batch != null) batch.dispose();
        if (font != null) font.dispose();
    }
}