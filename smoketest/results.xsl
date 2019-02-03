<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <!--<div id="resultsContainer">-->
        <!--test-->
        <!--</div>-->
        <div class="row" id="last-smoketest">
            Last Smoketest run at <xsl:value-of select="tests/allTestsStart/@allTestsStart"></xsl:value-of>
        </div>
        <div class="row headerRow">
            <h4>
            <div id="boo7" class="col-lg-2">Test Screen</div>
            <div id="boo8" class="col-lg-4">Test Name</div>
            <div id="boo9" class="col-lg-1">Result</div>
            <div id="boo10" class="col-lg-5">Reason</div>
            </h4>
        </div>

        <xsl:for-each select="tests/testScreen">
            <div class="row resultsRow small">
                <div class="col-lg-2 testScreen"> <xsl:value-of select="@testScreen"/></div>
                <div class="col-lg-4">
                    <ul>
                        <xsl:for-each select="error">
                            <xsl:choose>
                                <xsl:when test="string-length(@msg) > 1">
                                    <li class="test-fail">
                                        <xsl:value-of select="@testName"/>
                                    </li>
                                </xsl:when>
                                <xsl:otherwise>
                                    <li class="test-pass">
                                        <xsl:value-of select="@testName"/>
                                    </li>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:for-each>
                    </ul>
                </div>
                <div class="col-lg-1">
                    <ul>
                        <xsl:for-each select="error">
                            <xsl:choose>
                                <xsl:when test="string-length(@msg) > 1">
                                    <li class="test-fail">Fail</li>
                                </xsl:when>
                                <xsl:otherwise>
                                    <li class="test-pass">Pass</li>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:for-each>
                    </ul>

                </div>
                <div class="col-lg-5">
                    <ul>
                        <xsl:for-each select="error">
                            <xsl:choose>
                                <xsl:when test="string-length(@msg) > 1">
                                    <li class="test-fail">
                                        <xsl:value-of select="@msg"/>
                                    </li>
                                </xsl:when>
                                <xsl:otherwise>
                                    <li class="test-pass">
                                        <xsl:value-of select="@msg"/>
                                    </li>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:for-each>

                    </ul>

                </div>
            </div>
        </xsl:for-each>


        <!--<table class="table table-bordered">-->
                <!--<tr>-->
                    <!--<th>Test Screen</th>-->
                    <!--<th>Test Name</th>-->
                    <!--<th>Result</th>-->
                    <!--<th>Reason</th>-->
                <!--</tr>-->
        <!--</table>-->
        <!--<div id="resultsTable">-->
            <!--<div class="heading">CTR Smoke Tests results for <xsl:value-of select="smoketests/allTestsStart/@allTestsStart"></xsl:value-of>-->
            <!--</div>-->
            <!--<table border="1">-->
                <!--<tr>-->
                    <!--<th>Test Screen</th>-->
                    <!--<th>Test Name</th>-->
                    <!--<th>Result</th>-->
                    <!--<th>Reason</th>-->
                <!--</tr>-->

            <!--</table>-->
        <!--</div>-->
        <!--<div id="footer">footer</div>-->

    </xsl:template>
</xsl:stylesheet>