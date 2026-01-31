// core/src/io/hunterthecraft/pato/data/TileType.java
package io.hunterthecraft.pato.data;

public enum TileType {
    PLAIN("plain", "Campo", true),
    FOREST("forest", "Floresta", true),
    MOUNTAIN("mountain", "Montanha", false),
    WATER("water", "Água", false),
    RUINS("ruins", "Ruínas", true);

    public final String key;
    public final String name;
    public final boolean buildable;

    TileType(String key, String name, boolean buildable) {
        this.key = key;
        this.name = name;
        this.buildable = buildable;
    }
}