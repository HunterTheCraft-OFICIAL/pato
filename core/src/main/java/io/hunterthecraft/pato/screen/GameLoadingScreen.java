// core/src/io/hunterthecraft/pato/screen/GameLoadingScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.assets.AssetManager;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.viewport.ScreenViewport;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.scenes.scene2d.ui.ProgressBar;
import com.badlogic.gdx.scenes.scene2d.ui.Skin;
import com.badlogic.gdx.scenes.scene2d.ui.Table;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.data.TileType;

public class GameLoadingScreen implements Screen {
    private PatoGame game;
    private Stage stage;
    private AssetManager assetManager;
    private Label loadingLabel;
    private ProgressBar progressBar;
    private Skin skin;
    private BitmapFont font;

    public GameLoadingScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        stage = new Stage(new ScreenViewport());
        assetManager = new AssetManager();

        font = new BitmapFont(Gdx.files.internal("ui/font.fnt"));
        font.getData().setScale(1.0f);

        skin = new Skin();
        skin.add("default-font", font);
        skin.add("white", new Texture(Gdx.files.internal("ui/uiskin.png")));

        ProgressBar.ProgressBarStyle pbStyle = new ProgressBar.ProgressBarStyle();
        pbStyle.background = skin.newDrawable("white", 0.3f, 0.3f, 0.4f, 1);
        pbStyle.knobBefore = skin.newDrawable("white", 0.2f, 0.8f, 0.2f, 1);
        skin.add("default-horizontal", pbStyle);

        Label.LabelStyle labelStyle = new Label.LabelStyle(font, com.badlogic.gdx.graphics.Color.WHITE);
        skin.add("default", labelStyle);
        Table table = new Table();
        table.setFillParent(true);
        table.center();

        loadingLabel = new Label("Carregando mundo...", skin);
        table.add(loadingLabel).padBottom(20).row();

        progressBar = new ProgressBar(0, 100, 1, false, skin);
        progressBar.setWidth(300);
        table.add(progressBar).row();

        stage.addActor(table);

        // Carrega todos os tiles
        for (TileType type : TileType.values()) {
            assetManager.load(type.getAssetPath(), Texture.class);
        }
    }

    @Override
    public void render(float delta) {
        if (assetManager.update()) {
            game.setScreen(new GameScreen(game, assetManager));
            dispose();
            return;
        }

        float progress = assetManager.getProgress() * 100f;
        progressBar.setValue(progress);
        loadingLabel.setText("Carregando... " + (int)progress + "%");

        ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);
        stage.act(delta);
        stage.draw();
    }

    @Override
    public void resize(int width, int height) {
        stage.getViewport().update(width, height, true);
    }

    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}

    @Override
    public void dispose() {
        if (stage != null) stage.dispose();
        if (skin != null) skin.dispose();        if (font != null) font.dispose();
    }
}