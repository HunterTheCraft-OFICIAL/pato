// core/src/io/hunterthecraft/pato/screen/BugCenterScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.GlyphLayout;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.Clipboard;
import io.hunterthecraft.pato.PatoGame;

public class BugCenterScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private BitmapFont font;
    private GlyphLayout layout;
    private String fullLog;
    private boolean canCopy = false;

    public BugCenterScreen(PatoGame game, String log) {
        this.game = game;
        this.fullLog = log != null ? log : "Sem logs.";
    }

    @Override
    public void show() {
        batch = new SpriteBatch();
        font = new BitmapFont();
        font.getData().setScale(1.0f);
        layout = new GlyphLayout();
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.1f, 0.0f, 0.0f, 1); // vermelho escuro

        batch.begin();

        // Título
        font.setColor(Color.YELLOW);
        layout.setText(font, "❌ BUG CENTER");
        font.draw(batch, layout, 20, Gdx.graphics.getHeight() - 30);

        // Instruções
        font.setColor(Color.WHITE);
        layout.setText(font, "Toque na tela para copiar logs");
        font.draw(batch, layout, 20, 50);

        // Logs (simplificado)
        font.setColor(Color.RED);
        layout.setText(font, "Erro: " + (fullLog.length() > 100 ? fullLog.substring(0, 100) + "..." : fullLog));
        font.draw(batch, layout, 20, Gdx.graphics.getHeight() - 60);

        batch.end();

        // Copiar ao tocar
        if (Gdx.input.isTouched()) {
            if (!canCopy) {
                canCopy = true;
                Clipboard clipboard = Gdx.app.getClipboard();
                clipboard.setContents(fullLog);
            }
        } else {
            canCopy = false;
        }
    }

    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
    @Override public void dispose() {
        if (batch != null) batch.dispose();
        if (font != null) font.dispose();
    }
}