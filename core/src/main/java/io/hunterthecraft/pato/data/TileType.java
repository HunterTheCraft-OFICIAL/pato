// core/src/main/java/io/hunterthecraft/pato/data/TileType.java
package io.hunterthecraft.pato.data;

public enum TileType {
    AMAZONIA("debug_amazonia"),
    CERRADO("debug_cerrado");

    public final String key;

    TileType(String key) {
        this.key = key;
    }

    public String getAssetPath() {
        return "tiles/" + key + ".png";
    }
}