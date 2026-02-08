// core/src/io/hunterthecraft/pato/screen/WorldLoadingScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.files.FileHandle;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.Json;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.model.WorldData;

public class WorldLoadingScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private Json json;

    public WorldLoadingScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        batch = new SpriteBatch();
        json = new Json();

        // Carrega mundo em background
        Gdx.app.postRunnable(() -> {
            try {
                FileHandle file = Gdx.files.local("saves/current/world.json");
                if (!file.exists()) {
                    throw new RuntimeException("Arquivo world.json não encontrado!");
                }
                WorldData world = json.fromJson(WorldData.class, file.readString());
                game.setScreen(new GameScreen(game, world));
            } catch (Exception e) {
                Gdx.app.error("WorldLoading", "Falha ao carregar mundo", e);
                game.setScreen(new BugCenterScreen(game, e.toString()));
            }
        });
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.1f, 0.1f, 0.2f, 1); // azul escuro
        batch.begin();
        // Texto simples de carregamento
        float x = Gdx.graphics.getBackBufferWidth() / 2f - 100;
        float y = Gdx.graphics.getBackBufferHeight() / 2f;
        batch.setColor(1, 1, 1, 1);
        // Desenha texto branco (sem fonte, só retângulo)
        batch.draw(batch.getTexture(), x, y, 200, 30);
        batch.end();
    }

    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
    @Override public void dispose() {
        if (batch != null) batch.dispose();
    }
}