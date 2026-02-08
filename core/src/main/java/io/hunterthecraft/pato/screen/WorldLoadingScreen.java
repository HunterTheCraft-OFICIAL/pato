// core/src/main/java/io/hunterthecraft/pato/screen/WorldLoadingScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.files.FileHandle;
import com.badlogic.gdx.utils.Json;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.model.WorldData;

public class WorldLoadingScreen implements Screen {
    private PatoGame game;
    private Json json;

    public WorldLoadingScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        json = new Json();

        Gdx.app.postRunnable(() -> {
            try {
                FileHandle file = Gdx.files.local("saves/current/world.json");
                if (!file.exists()) {
                    throw new RuntimeException("world.json não encontrado!");
                }
                WorldData world = json.fromJson(WorldData.class, file.readString());
                game.setScreen(new GameScreen(game, world));
            } catch (Exception e) {
                game.setScreen(new BugCenterScreen(game, e.toString()));
            }
        });
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.1f, 0.1f, 0.2f, 1); // só fundo azul
    }

    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
    @Override public void dispose() {}
}