<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="tests/errorCount/@errorCount &gt; 0">
                <!--<h1 class="test-fail">Fail</h1>-->
                <div class="test-fail">
                    <h1>Fail</h1>
                </div>
            </xsl:when>
            <xsl:otherwise>
                <div class="test-pass">
                    <h1>Pass</h1>
                </div>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
