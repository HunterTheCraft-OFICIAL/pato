// core/src/io/hunterthecraft/pato/renderer/UiRenderer.java
package io.hunterthecraft.pato.renderer;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.Pixmap;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.GlyphLayout;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.Disposable;
import io.hunterthecraft.pato.data.TileType;

public class UiRenderer implements Disposable {
    private SpriteBatch batch;
    private BitmapFont font;
    private GlyphLayout layout;
    private Texture whitePixel;

    public UiRenderer(SpriteBatch batch) {
        this.batch = batch;
        this.font = new BitmapFont();
        this.font.getData().setScale(1.0f);
        this.layout = new GlyphLayout();
        createWhitePixel();
    }

    private void createWhitePixel() {
        Pixmap pixmap = new Pixmap(1, 1, Pixmap.Format.RGBA8888);
        pixmap.setColor(Color.WHITE);
        pixmap.fill();
        whitePixel = new Texture(pixmap);
        pixmap.dispose();
    }

    public void drawPauseButton() {
        float size = 128; // Tamanho de um tile
        float btnX = Gdx.graphics.getWidth() - size;
        float btnY = Gdx.graphics.getHeight() - size;
        
        // Fundo do botão
        batch.setColor(0.2f, 0.2f, 0.3f, 0.8f);
        batch.draw(whitePixel, btnX, btnY, size, size);
        
        // Ícone grande
        batch.setColor(1, 1, 1, 1);
        font.setColor(Color.WHITE);
        font.getData().setScale(4.0f); // Texto grande
        layout.setText(font, "⏸");
        font.draw(batch, layout,             btnX + size/2f - layout.width/2f,
            btnY + size/2f + layout.height/2f
        );
        font.getData().setScale(1.0f); // Restaura escala
    }

    public void drawTilePopup(int tileX, int tileY, TileType tileType) {
        float px = tileX * 128;
        float py = tileY * 128 + 128;

        batch.setColor(0, 0, 0, 0.7f);
        batch.draw(whitePixel, px, py, 200, 100);
        batch.setColor(1, 1, 1, 1);

        font.setColor(Color.WHITE);
        layout.setText(font, "Bioma: " + tileType.toString());
        font.draw(batch, layout, px + 10, py + 80);

        layout.setText(font, String.format("Coord: (%d, %d)", tileX, tileY));
        font.draw(batch, layout, px + 10, py + 60);

        layout.setText(font, "✕");
        font.draw(batch, layout, px + 180, py + 90);
    }

    public void drawPauseMenu() {
        batch.setColor(0, 0, 0, 0.6f);
        batch.draw(whitePixel, 0, 0, Gdx.graphics.getWidth(), Gdx.graphics.getHeight());
        batch.setColor(1, 1, 1, 1);

        font.setColor(Color.YELLOW);
        layout.setText(font, "PAUSA");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 80);

        font.setColor(Color.WHITE);
        layout.setText(font, "Continuar");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 120);

        layout.setText(font, "Menu Principal");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 160);

        layout.setText(font, "Configurações");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 200);

        layout.setText(font, "Sair");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 240);
    }

    public void drawSettingsMenu(
        boolean invertScrollY,        boolean invertPinch,
        float pinchSensitivity,
        float scrollSensitivity
    ) {
        batch.setColor(0, 0, 0, 0.7f);
        batch.draw(whitePixel, 50, 50, Gdx.graphics.getWidth() - 100, Gdx.graphics.getHeight() - 100);
        batch.setColor(1, 1, 1, 1);

        font.setColor(Color.YELLOW);
        layout.setText(font, "CONTROLES");
        font.draw(batch, layout, 100, Gdx.graphics.getHeight() - 100);

        int y = Gdx.graphics.getHeight() - 140;

        String scrollText = "Inverter Eixo Y: " + (invertScrollY ? "SIM" : "NÃO");
        layout.setText(font, scrollText);
        font.draw(batch, layout, 100, y);
        y -= 40;

        String pinchText = "Inverter Pinça: " + (invertPinch ? "SIM" : "NÃO");
        layout.setText(font, pinchText);
        font.draw(batch, layout, 100, y);
        y -= 40;

        String pinchSensText = "Sens. Pinça: " + String.format("%.4f", pinchSensitivity);
        layout.setText(font, pinchSensText);
        font.draw(batch, layout, 100, y);
        y -= 40;

        String scrollSensText = "Sens. Scroll: " + String.format("%.2f", scrollSensitivity);
        layout.setText(font, scrollSensText);
        font.draw(batch, layout, 100, y);
    }

    @Override
    public void dispose() {
        if (whitePixel != null) whitePixel.dispose();
        if (font != null) font.dispose();
    }
}