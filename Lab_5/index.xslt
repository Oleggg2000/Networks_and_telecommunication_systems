<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head>
                <meta charset="utf-8" />
                <title>Астрономия</title>
            </head>
            <body>
                <h1>Вот это астрономия)</h1>
                <div><xsl:for-each select="/universe"><xsl:value-of select="timer"/></xsl:for-each></div>
                <table border="1">
                    <tr>
                        <th>Галактика: </th>
                        <td><xsl:for-each select="/universe/galaxies/MilkyWay"><xsl:value-of select="name"/></xsl:for-each></td>
                        <th>Планеты: </th>
                        <xsl:for-each select="/universe/galaxies/MilkyWay/planets/planet">
                            <td><xsl:value-of select="name"/></td>
                        </xsl:for-each>
                    </tr>
                    <tr>
                        <th>Галактика: </th>
                        <td><xsl:for-each select="/universe/galaxies/LargeMagellanicCloud"><xsl:value-of select="name"/></xsl:for-each></td>
                        <th>Звезды: </th>
                        <xsl:for-each select="/universe/galaxies/LargeMagellanicCloud/stars/star">
                            <td><xsl:value-of select="name"/></td>
                        </xsl:for-each>
                    </tr>
                    <tr>
                        <th>Галактика: </th>
                        <td><xsl:for-each select="/universe/galaxies/SmallMagellanicCloud"><xsl:value-of select="name"/></xsl:for-each></td>
                        <th>Звезды: </th>
                        <xsl:for-each select="/universe/galaxies/SmallMagellanicCloud/stars/star">
                            <td><xsl:value-of select="name"/></td>
                        </xsl:for-each>
                    </tr>
                    <tr>
                        <th>Галактика: </th>
                        <td><xsl:for-each select="/universe/galaxies/AndromedaGalaxy"><xsl:value-of select="name"/></xsl:for-each></td>
                        <th>Звезды: </th>
                        <xsl:for-each select="/universe/galaxies/AndromedaGalaxy/stars/star">
                            <td><xsl:value-of select="name"/></td>
                        </xsl:for-each>
                    </tr>
                    <tr>
                        <th>Галактика: </th>
                        <td><xsl:for-each select="/universe/galaxies/TriangulumGalaxy"><xsl:value-of select="name"/></xsl:for-each></td>
                        <th>Звезды: </th>
                        <xsl:for-each select="/universe/galaxies/TriangulumGalaxy/stars/star">
                            <td><xsl:value-of select="name"/></td>
                        </xsl:for-each>
                    </tr>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>