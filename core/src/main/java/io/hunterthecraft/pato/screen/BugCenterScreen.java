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
    private boolean touched = false;

    public BugCenterScreen(PatoGame game, String log) {
        this.game = game;
        this.fullLog = log != null ? log : "Sem logs disponíveis.";
    }

    @Override
    public void show() {
        batch = new SpriteBatch();
        font = new BitmapFont();
        font.getData().setScale(1.2f);
        layout = new GlyphLayout();
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.2f, 0.0f, 0.0f, 1); // vermelho escuro

        batch.begin();

        // Título
        font.setColor(Color.YELLOW);
        layout.setText(font, "❌ BUG CENTER");
        font.draw(batch, layout, 20, Gdx.graphics.getBackBufferHeight() - 30);

        // Área de logs (texto exato que você pediu)
        font.setColor(Color.WHITE);
        String logText = "Todos os logs gerados,\nmesmo que o relevante para\ntemos visão total";
        layout.setText(font, logText, Color.WHITE, Gdx.graphics.getBackBufferWidth() - 200, 0, true);
        font.draw(batch, layout, 180, Gdx.graphics.getBackBufferHeight() - 80);
        // Botão: Menu
        font.setColor(Color.WHITE);
        layout.setText(font, "Menu");
        float btnX = 20;
        float btnY = Gdx.graphics.getBackBufferHeight() - 120;
        font.draw(batch, layout, btnX, btnY);
        checkButtonTap(btnX, btnY - layout.height, layout.width, layout.height + 10, () -> {
            game.setScreen(new StartupScreen(game));
        });

        // Botão: Copiar
        layout.setText(font, "Copiar");
        float copyY = Gdx.graphics.getBackBufferHeight() - 180;
        font.draw(batch, layout, btnX, copyY);
        checkButtonTap(btnX, copyY - layout.height, layout.width, layout.height + 10, () -> {
            Clipboard clipboard = Gdx.app.getClipboard();
            clipboard.setContents(fullLog);
        });

        // Botão: Sair
        layout.setText(font, "Sair");
        float exitY = Gdx.graphics.getBackBufferHeight() - 240;
        font.draw(batch, layout, btnX, exitY);
        checkButtonTap(btnX, exitY - layout.height, layout.width, layout.height + 10, () -> {
            Gdx.app.exit();
        });

        batch.end();
    }

    private void checkButtonTap(float x, float y, float width, float height, Runnable action) {
        if (Gdx.input.isTouched()) {
            float touchX = Gdx.input.getX();
            float touchY = Gdx.graphics.getBackBufferHeight() - Gdx.input.getY();
            if (!touched && touchX >= x && touchX <= x + width && touchY >= y && touchY <= y + height) {
                touched = true;
                action.run();
            }
        } else {
            touched = false;
        }
    }

    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
    @Override public void dispose() {
        if (batch != null) batch.dispose();        if (font != null) font.dispose();
    }
}