// core/src/io/hunterthecraft/pato/screen/MainMenuScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.GlyphLayout;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;

public class MainMenuScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private BitmapFont font;
    private GlyphLayout layout;
    private boolean touched = false;

    public MainMenuScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        batch = new SpriteBatch();
        font = new BitmapFont();
        font.getData().setScale(2.0f);
        layout = new GlyphLayout();
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);

        batch.begin();

        // Título
        font.setColor(Color.YELLOW);
        layout.setText(font, "MENU PRINCIPAL");
        float titleX = Gdx.graphics.getBackBufferWidth() / 2f - layout.width / 2f;
        font.draw(batch, layout, titleX, Gdx.graphics.getBackBufferHeight() - 50);

        // Botão 1: Iniciar Jogo
        font.setColor(Color.WHITE);
        layout.setText(font, "Iniciar Jogo");
        float btn1X = Gdx.graphics.getBackBufferWidth() / 2f - layout.width / 2f;
        float btn1Y = Gdx.graphics.getBackBufferHeight() / 2f + 60;
        font.draw(batch, layout, btn1X, btn1Y);
        checkButtonTap(btn1X, btn1Y - layout.height, layout.width, layout.height + 10, () -> {
            // Futuro: GameLoadingScreen
            game.setScreen(new WorldLoadingScreen(game));
            //game.setScreen(new BugCenterScreen(game, "Jogo ainda não implementado."));
        });

        // Botão 2: Sair
        layout.setText(font, "Sair");
        float btn2X = Gdx.graphics.getBackBufferWidth() / 2f - layout.width / 2f;
        float btn2Y = Gdx.graphics.getBackBufferHeight() / 2f - 20;
        font.draw(batch, layout, btn2X, btn2Y);
        checkButtonTap(btn2X, btn2Y - layout.height, layout.width, layout.height + 10, () -> {
            Gdx.app.exit();
        });

        // Botão 3: Forçar Erro (BugCenter)
        layout.setText(font, "Forçar Erro");
        float btn3X = Gdx.graphics.getBackBufferWidth() / 2f - layout.width / 2f;
        float btn3Y = Gdx.graphics.getBackBufferHeight() / 2f - 100;
        font.draw(batch, layout, btn3X, btn3Y);
        checkButtonTap(btn3X, btn3Y - layout.height, layout.width, layout.height + 10, () -> {
            game.setScreen(new BugCenterScreen(game, "Erro forçado pelo usuário.\nEste é um log de teste."));
        });

        batch.end();
    }

    private void checkButtonTap(float x, float y, float width, float height, Runnable action) {
        if (Gdx.input.isTouched()) {
            float touchX = Gdx.input.getX();
            float touchY = Gdx.graphics.getBackBufferHeight() - Gdx.input.getY(); // inverte Y
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
        if (batch != null) batch.dispose();
        if (font != null) font.dispose();
    }
}