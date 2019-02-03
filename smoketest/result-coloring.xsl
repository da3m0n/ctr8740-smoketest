<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="tests/errorCount/@errorCount &gt; 0">
                <div class="test-fail">
                    Failed
                </div>
            </xsl:when>
            <xsl:otherwise>
                <div class="test-pass">
                    Passed
                </div>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
