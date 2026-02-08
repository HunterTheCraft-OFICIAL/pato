// core/src/io/hunterthecraft/pato/PatoGame.java
package io.hunterthecraft.pato;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.GlyphLayout;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.screen.StartupScreen; // ← IMPORT ESSENCIAL

public class PatoGame extends Game {
    private SpriteBatch batch;
    private BitmapFont font;
    private GlyphLayout layout;
    private float timer = 0f;

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
        timer += Gdx.graphics.getDeltaTime();
        
        if (timer < 1.0f) {
            ScreenUtils.clear(0, 0, 0.2f, 1);
            String text = "PATO FUNCIONANDO!";
            layout.setText(font, text);
            float x = Gdx.graphics.getBackBufferWidth() / 2f - layout.width / 2f;
            float y = Gdx.graphics.getBackBufferHeight() / 2f + layout.height / 2f;
            batch.begin();
            font.draw(batch, layout, x, y);
            batch.end();
        } else {
            setScreen(new StartupScreen(this));
        }
    }

    @Override
    public void dispose() {
        if (batch != null) batch.dispose();
        if (font != null) font.dispose();
    }
}