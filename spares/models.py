# coding=utf-8
from django.core.urlresolvers import reverse
from spares import settings
from django.db import models, connection

CCarModelsSQL = """
        SELECT
            MOD_ID AS id,
            TEX_TEXT AS name,
            MOD_PCON_START as startMan,
            MOD_PCON_END as endMan,
            MFA_BRAND as brand
        FROM
            """ + settings.TD_PREFIX + """.MODELS
            INNER JOIN """ + settings.TD_PREFIX + """.MANUFACTURERS ON MFA_ID = MOD_MFA_ID
            INNER JOIN """ + settings.TD_PREFIX + """.COUNTRY_DESIGNATIONS ON CDS_ID = MOD_CDS_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON TEX_ID = CDS_TEX_ID
        WHERE
            MOD_MFA_ID = %s AND
            CDS_LNG_ID = %s
    """

CCarVariantsSQL = """
        SELECT
                TYP_ID as id,
                TYP_MOD_ID as modelId,
                DES_TEXTS.TEX_TEXT AS name,
                TYP_PCON_START as startMan,
                TYP_PCON_END as endMan,
                TYP_CCM as volume,
                TYP_KW_FROM as kw,
                TYP_HP_FROM as hp,
                TYP_CYLINDERS as cylinders,
                TYP_LITRES as litres,
                TYP_VALVES as valves,
                ENGINES.ENG_CODE as engineCode,
                DES_TEXTS2.TEX_TEXT as engine,
                DES_TEXTS3.TEX_TEXT as fuel,
                IFNULL(DES_TEXTS4.TEX_TEXT, DES_TEXTS5.TEX_TEXT) AS body,
                DES_TEXTS6.TEX_TEXT AS fuelSupply,
                DES_TEXTS7.TEX_TEXT as drive,
                TYP_MAX_WEIGHT as weight,
                DES_TEXTS9.TEX_TEXT AS modelName
            FROM
                           """ + settings.TD_PREFIX + """.TYPES
                INNER JOIN """ + settings.TD_PREFIX + """.MODELS ON MOD_ID = TYP_MOD_ID
                INNER JOIN """ + settings.TD_PREFIX + """.COUNTRY_DESIGNATIONS ON COUNTRY_DESIGNATIONS.CDS_ID = TYP_MMT_CDS_ID
                INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON DES_TEXTS.TEX_ID = COUNTRY_DESIGNATIONS.CDS_TEX_ID
                INNER JOIN """ + settings.TD_PREFIX + """.COUNTRY_DESIGNATIONS AS COUNTRY_DESIGNATIONS2 ON COUNTRY_DESIGNATIONS2.CDS_ID = MOD_CDS_ID
                INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS9 ON DES_TEXTS9.TEX_ID = COUNTRY_DESIGNATIONS2.CDS_TEX_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS ON DESIGNATIONS.DES_ID = TYP_KV_ENGINE_DES_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS2 ON DES_TEXTS2.TEX_ID = DESIGNATIONS.DES_TEX_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS2 ON DESIGNATIONS2.DES_ID = TYP_KV_FUEL_DES_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS3 ON DES_TEXTS3.TEX_ID = DESIGNATIONS2.DES_TEX_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.LINK_TYP_ENG ON LTE_TYP_ID = TYP_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.ENGINES ON ENG_ID = LTE_ENG_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS3 ON DESIGNATIONS3.DES_ID = TYP_KV_BODY_DES_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS4 ON DES_TEXTS4.TEX_ID = DESIGNATIONS3.DES_TEX_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS4 ON DESIGNATIONS4.DES_ID = TYP_KV_MODEL_DES_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS5 ON DES_TEXTS5.TEX_ID = DESIGNATIONS4.DES_TEX_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS5 ON DESIGNATIONS5.DES_ID = TYP_KV_FUEL_DES_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS6 ON DES_TEXTS6.TEX_ID = DESIGNATIONS5.DES_TEX_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS6 ON DESIGNATIONS6.DES_ID = TYP_KV_DRIVE_DES_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS7 ON DES_TEXTS7.TEX_ID = DESIGNATIONS6.DES_TEX_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.COUNTRY_DESIGNATIONS AS DESIGNATIONS7 ON DESIGNATIONS7.CDS_ID = TYP_MMT_CDS_ID
                LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS8 ON DES_TEXTS8.TEX_ID = DESIGNATIONS7.CDS_TEX_ID
            WHERE
                TYP_MOD_ID = %(mod_id)s AND
                COUNTRY_DESIGNATIONS.CDS_LNG_ID = %(lng_id)s AND
                COUNTRY_DESIGNATIONS2.CDS_LNG_ID = %(lng_id)s AND
                (DESIGNATIONS.DES_LNG_ID IS NULL OR DESIGNATIONS.DES_LNG_ID = %(lng_id)s) AND
                (DESIGNATIONS2.DES_LNG_ID IS NULL OR DESIGNATIONS2.DES_LNG_ID = %(lng_id)s) AND
                (DESIGNATIONS3.DES_LNG_ID IS NULL OR DESIGNATIONS3.DES_LNG_ID = %(lng_id)s) AND
                (DESIGNATIONS4.DES_LNG_ID IS NULL OR DESIGNATIONS4.DES_LNG_ID = %(lng_id)s) AND
                (DESIGNATIONS5.DES_LNG_ID IS NULL OR DESIGNATIONS5.DES_LNG_ID = %(lng_id)s) AND
                (DESIGNATIONS6.DES_LNG_ID IS NULL OR DESIGNATIONS6.DES_LNG_ID = %(lng_id)s) AND
                (DESIGNATIONS7.CDS_LNG_ID IS NULL OR DESIGNATIONS7.CDS_LNG_ID = %(lng_id)s)
    """

CStrTreeSQL = """
        SELECT
            STR_ID AS id,
            CONCAT(UCASE(LEFT(TEX_TEXT, 1)), SUBSTRING(TEX_TEXT, 2)) AS text,
            IF(
                EXISTS(
                    SELECT
                        *
                    FROM
                        """ + settings.TD_PREFIX + """.SEARCH_TREE AS SEARCH_TREE2
                    WHERE
                        SEARCH_TREE2.STR_ID_PARENT <=> """ + settings.TD_PREFIX + """.SEARCH_TREE.STR_ID
                    LIMIT
                        1
                ), 1, 0) AS leaf
        FROM
                       """ + settings.TD_PREFIX + """.SEARCH_TREE
            INNER JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS ON DES_ID = STR_DES_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON TEX_ID = DES_TEX_ID
        WHERE
            STR_ID_PARENT <=> 10001 AND
            DES_LNG_ID = %(lng_id)s AND
            EXISTS (
                SELECT
                    *
                FROM
                               """ + settings.TD_PREFIX + """.LINK_GA_STR
                    INNER JOIN """ + settings.TD_PREFIX + """.LINK_LA_TYP ON LAT_TYP_ID = %(type_id)s AND
                                              LAT_GA_ID = LGS_GA_ID
                    INNER JOIN """ + settings.TD_PREFIX + """.LINK_ART ON LA_ID = LAT_LA_ID
                WHERE
                    LGS_STR_ID = STR_ID
                LIMIT
                    1
            )
        ORDER BY
            leaf desc, STR_SORT
    """

CStrTreeSQLStrId = """
        SELECT
            STR_ID AS id,
            CONCAT(UCASE(LEFT(TEX_TEXT, 1)), SUBSTRING(TEX_TEXT, 2)) AS text,
            IF(
                EXISTS(
                    SELECT
                        *
                    FROM
                        """ + settings.TD_PREFIX + """.SEARCH_TREE AS SEARCH_TREE2
                    WHERE
                        SEARCH_TREE2.STR_ID_PARENT <=> """ + settings.TD_PREFIX + """.SEARCH_TREE.STR_ID
                    LIMIT
                        1
                ), 1, 0) AS leaf
        FROM
                       """ + settings.TD_PREFIX + """.SEARCH_TREE
            INNER JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS ON DES_ID = STR_DES_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON TEX_ID = DES_TEX_ID
        WHERE
            STR_ID_PARENT = %(str_id)s AND
            DES_LNG_ID = %(lng_id)s AND
            EXISTS (
                SELECT
                    *
                FROM
                               """ + settings.TD_PREFIX + """.LINK_GA_STR
                    INNER JOIN """ + settings.TD_PREFIX + """.LINK_LA_TYP ON LAT_TYP_ID = %(type_id)s AND
                                              LAT_GA_ID = LGS_GA_ID
                    INNER JOIN """ + settings.TD_PREFIX + """.LINK_ART ON LA_ID = LAT_LA_ID
                WHERE
                    LGS_STR_ID = STR_ID
                LIMIT
                    1
            )
        ORDER BY
            leaf desc, STR_SORT
    """

CStrTreeSQLGetStrId = """
        SELECT
            STR_ID AS id,
            CONCAT(UCASE(LEFT(TEX_TEXT, 1)), SUBSTRING(TEX_TEXT, 2)) AS text
        FROM
                       """ + settings.TD_PREFIX + """.SEARCH_TREE
            INNER JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS ON DES_ID = STR_DES_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON TEX_ID = DES_TEX_ID
        WHERE
            STR_ID = %(str_id)s AND
            DES_LNG_ID = %(lng_id)s
        LIMIT 1
    """

CSparesListBySupplierSQL = """
        SELECT
                ART_ID as id,
                ART_ARTICLE_NR as article,
                SUP_BRAND as supBrand,
                DES_TEXTS.TEX_TEXT AS as name
            FROM
                           """ + settings.TD_PREFIX + """.ARTICLES
                INNER JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS ON """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_ID = ART_COMPLETE_DES_ID
                INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON DES_TEXTS.TEX_ID = """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_TEX_ID
                INNER JOIN """ + settings.TD_PREFIX + """.SUPPLIERS ON SUP_ID = ART_SUP_ID
                INNER JOIN " . PREFIX . "spares ON ITEM_ARTICLE = ART_ARTICLE_NR
                INNER JOIN " . PREFIX . "spares_suppliers sup ON sup.SUP_ID = ITEM_SUP_ID
            WHERE
                SUP_BRAND = '" . $site->my_str_replace($sup_brand) . "' AND
                DES_TEXTS.TEX_TEXT = '" . $site->my_str_replace($art_des_text) . "' AND
                DESIGNATIONS.DES_LNG_ID = " . $_SESSION['CMS_LNG_ID'] . "
    """

CSparesListByStrSQL = """
         SELECT
            ART_ID as id,
            ART_ARTICLE_NR as article,
            SUP_BRAND as supBrand,
            DES_TEXTS.TEX_TEXT AS name
        FROM
                       """ + settings.TD_PREFIX + """.LINK_GA_STR
            INNER JOIN """ + settings.TD_PREFIX + """.LINK_LA_TYP ON LAT_TYP_ID = %(typ_id)s AND
                                      LAT_GA_ID = LGS_GA_ID
            INNER JOIN """ + settings.TD_PREFIX + """.LINK_ART ON LA_ID = LAT_LA_ID
            INNER JOIN """ + settings.TD_PREFIX + """.ARTICLES ON ART_ID = LA_ART_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS ON """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_ID = ART_COMPLETE_DES_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON DES_TEXTS.TEX_ID = """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_TEX_ID
            INNER JOIN """ + settings.TD_PREFIX + """.SUPPLIERS ON SUP_ID = ART_SUP_ID
            INNER JOIN """ + settings.TD_PREFIX + """.ART_COUNTRY_SPECIFICS ON ACS_ART_ID = ART_ID
        WHERE
            LGS_STR_ID = %(str_id)s AND
            DESIGNATIONS.DES_LNG_ID = %(lng_id)s
        ORDER BY
            supBrand,
            name,
            article
    """

CSparesListByArtSQL = """
         SELECT
            ART_ID as id,
            ART_ARTICLE_NR as article,
            SUP_BRAND as supBrand,
            DES_TEXTS.TEX_TEXT AS name
        FROM
                       """ + settings.TD_PREFIX + """.ARTICLES
            INNER JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS ON """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_ID = ART_COMPLETE_DES_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON DES_TEXTS.TEX_ID = """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_TEX_ID
            INNER JOIN """ + settings.TD_PREFIX + """.SUPPLIERS ON SUP_ID = ART_SUP_ID
            INNER JOIN """ + settings.TD_PREFIX + """.ART_COUNTRY_SPECIFICS ON ACS_ART_ID = ART_ID
        WHERE
            ART_ARTICLE_NR = %(article)s AND
            DESIGNATIONS.DES_LNG_ID = %(lng_id)s
        LIMIT 1
    """

CSparesCriteriaSQL = """
        SELECT
            DISTINCT ACR_SORT,
            DES_TEXTS.TEX_TEXT AS CRITERIA_DES_TEXT,
            IFNULL(DES_TEXTS2.TEX_TEXT, ACR_VALUE) AS CRITERIA_VALUE_TEXT
        FROM
                      """ + settings.TD_PREFIX + """.ARTICLE_CRITERIA
            LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS2 ON DESIGNATIONS2.DES_ID = ACR_KV_DES_ID
            LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS2 ON DES_TEXTS2.TEX_ID = DESIGNATIONS2.DES_TEX_ID
            LEFT JOIN """ + settings.TD_PREFIX + """.CRITERIA ON CRI_ID = ACR_CRI_ID
            LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS ON """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_ID = CRI_DES_ID
            LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON """ + settings.TD_PREFIX + """.DES_TEXTS.TEX_ID = """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_TEX_ID
        WHERE
            ACR_ART_ID = %(art_id)s AND
            (DESIGNATIONS.DES_LNG_ID IS NULL OR DESIGNATIONS.DES_LNG_ID = %(lng_id)s) AND
            (DESIGNATIONS2.DES_LNG_ID IS NULL OR DESIGNATIONS2.DES_LNG_ID = %(lng_id)s)
    """

CSparesImagesSQL = """
        SELECT
            GRA_GRD_ID,
            CONCAT(
                '""" + settings.STATIC_URL + """/spares/',
                GRA_TAB_NR, '/',
                GRA_GRD_ID, '.',
                IF(LOWER(DOC_EXTENSION)='jp2', 'jpg', LOWER(DOC_EXTENSION))
            ) AS PATH
        FROM
                       """ + settings.TD_PREFIX + """.LINK_GRA_ART
            INNER JOIN """ + settings.TD_PREFIX + """.GRAPHICS ON GRA_ID = LGA_GRA_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DOC_TYPES ON DOC_TYPE = GRA_DOC_TYPE
        WHERE
            LGA_ART_ID = %(art_id)s AND
            (GRA_LNG_ID = %(lng_id)s OR GRA_LNG_ID = 255) AND
            GRA_DOC_TYPE <> 2
        ORDER BY
            GRA_GRD_ID
    """

CSparesApplicablesSQL = """
        SELECT
            TYP_ID as id,
            TYP_MOD_ID as modelId,
            DES_TEXTS.TEX_TEXT AS name,
            TYP_PCON_START as startMan,
            TYP_PCON_END as endMan,
            TYP_CCM as volume,
            TYP_KW_FROM as kw,
            TYP_HP_FROM as hp,
            TYP_CYLINDERS as cylinders,
            TYP_LITRES as litres,
            TYP_VALVES as valves,
            ENGINES.ENG_CODE as engineCode,
            DES_TEXTS2.TEX_TEXT as engine,
            DES_TEXTS3.TEX_TEXT as fuel,
            IFNULL(DES_TEXTS4.TEX_TEXT, DES_TEXTS5.TEX_TEXT) AS body,
            MFA_BRAND,
            DES_TEXTS7.TEX_TEXT AS modelName,
            DES_TEXTS8.TEX_TEXT as drive
        FROM
                       """ + settings.TD_PREFIX + """.LINK_ART
            INNER JOIN """ + settings.TD_PREFIX + """.LINK_LA_TYP ON LAT_LA_ID = LA_ID
            INNER JOIN """ + settings.TD_PREFIX + """.TYPES ON TYP_ID = LAT_TYP_ID
            INNER JOIN """ + settings.TD_PREFIX + """.COUNTRY_DESIGNATIONS ON """ + settings.TD_PREFIX + """.COUNTRY_DESIGNATIONS.CDS_ID = TYP_MMT_CDS_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS ON DES_TEXTS.TEX_ID = """ + settings.TD_PREFIX + """.COUNTRY_DESIGNATIONS.CDS_TEX_ID
            INNER JOIN """ + settings.TD_PREFIX + """.MODELS ON MOD_ID = TYP_MOD_ID
            INNER JOIN """ + settings.TD_PREFIX + """.MANUFACTURERS ON MFA_ID = MOD_MFA_ID
            INNER JOIN """ + settings.TD_PREFIX + """.COUNTRY_DESIGNATIONS AS COUNTRY_DESIGNATIONS2 ON COUNTRY_DESIGNATIONS2.CDS_ID = MOD_CDS_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS7 ON DES_TEXTS7.TEX_ID = COUNTRY_DESIGNATIONS2.CDS_TEX_ID
            INNER JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS7 ON DESIGNATIONS7.DES_ID = TYP_KV_DRIVE_DES_ID
             INNER JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS8 ON DES_TEXTS8.TEX_ID = DESIGNATIONS7.DES_TEX_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS ON """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_ID = TYP_KV_ENGINE_DES_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS2 ON DES_TEXTS2.TEX_ID = """ + settings.TD_PREFIX + """.DESIGNATIONS.DES_TEX_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS2 ON DESIGNATIONS2.DES_ID = TYP_KV_FUEL_DES_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS3 ON DES_TEXTS3.TEX_ID = DESIGNATIONS2.DES_TEX_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.LINK_TYP_ENG ON LTE_TYP_ID = TYP_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.ENGINES ON ENG_ID = LTE_ENG_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS3 ON DESIGNATIONS3.DES_ID = TYP_KV_BODY_DES_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS4 ON DES_TEXTS4.TEX_ID = DESIGNATIONS3.DES_TEX_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS4 ON DESIGNATIONS4.DES_ID = TYP_KV_MODEL_DES_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS5 ON DES_TEXTS5.TEX_ID = DESIGNATIONS4.DES_TEX_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DESIGNATIONS AS DESIGNATIONS5 ON DESIGNATIONS5.DES_ID = TYP_KV_AXLE_DES_ID
             LEFT JOIN """ + settings.TD_PREFIX + """.DES_TEXTS AS DES_TEXTS6 ON DES_TEXTS6.TEX_ID = DESIGNATIONS5.DES_TEX_ID

        WHERE
            LA_ART_ID = %(art_id)s AND
            MFA_BRAND = %(brand)s AND
            COUNTRY_DESIGNATIONS.CDS_LNG_ID = %(lng_id)s AND
            COUNTRY_DESIGNATIONS2.CDS_LNG_ID = %(lng_id)s AND
            (DESIGNATIONS.DES_LNG_ID IS NULL OR DESIGNATIONS.DES_LNG_ID = %(lng_id)s) AND
            (DESIGNATIONS2.DES_LNG_ID IS NULL OR DESIGNATIONS2.DES_LNG_ID = %(lng_id)s) AND
            (DESIGNATIONS3.DES_LNG_ID IS NULL OR DESIGNATIONS3.DES_LNG_ID = %(lng_id)s) AND
            (DESIGNATIONS4.DES_LNG_ID IS NULL OR DESIGNATIONS4.DES_LNG_ID = %(lng_id)s) AND
            (DESIGNATIONS5.DES_LNG_ID IS NULL OR DESIGNATIONS5.DES_LNG_ID = %(lng_id)s) AND
            (DESIGNATIONS7.DES_LNG_ID IS NULL OR DESIGNATIONS7.DES_LNG_ID = %(lng_id)s)
        GROUP BY
            TYP_ID
        ORDER BY
            MFA_BRAND,
            modelName,
            name,
            startMan,
            volume
    """


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class CSparesCarModelsManager(models.Manager):
    def list(self):
        return CCarModels.objects.raw(CCarModelsSQL + ' ORDER BY name', [settings.MOD_MFA_ID, settings.CDS_LNG_ID])

    def listByLetter(self, letter):
        return CCarModels.objects.raw(
            CCarModelsSQL + ' AND TEX_TEXT like "' + letter + '%%" ORDER BY startMan desc, name',
            [settings.MOD_MFA_ID, settings.CDS_LNG_ID])

    def findByTitle(self, title):
        title = title.replace('_', ' ')
        cursor = connection.cursor()
        cursor.execute(CCarModelsSQL + """ AND TEX_TEXT like '%%""" + title + """%%'""",
                       [settings.MOD_MFA_ID, settings.CDS_LNG_ID])
        row = dictfetchall(cursor)
        return CCarModels(**row[0])

    def listRandomRecs(self, count):
        return CCarModels.objects.raw(CCarModelsSQL + ' ORDER BY RAND(), name LIMIT 0, ' + str(count),
                                      [settings.MOD_MFA_ID, settings.CDS_LNG_ID])


class CSparesCarVariantsManager(models.Manager):
    def list(self, modelId):
        return CCarVariants.objects.raw(
            CCarVariantsSQL + " ORDER BY name, TYP_PCON_START, TYP_CCM",
            {'lng_id': settings.CDS_LNG_ID, 'mod_id': modelId}
        )

    def findById(self, modelId, variant):
        cursor = connection.cursor()
        cursor.execute(CCarVariantsSQL + " AND TYP_ID = " + variant + " ORDER BY name, TYP_PCON_START, TYP_CCM",
                       {'lng_id': settings.CDS_LNG_ID, 'mod_id': modelId})
        row = dictfetchall(cursor)
        return CCarVariants(**row[0])


class CSparesStrTreeManager(models.Manager):
    def list(self, typeId, strId):
        cursor = connection.cursor()
        cursor.execute(CStrTreeSQL if int(strId) == 0 else CStrTreeSQLStrId,
                       {'lng_id': settings.CDS_LNG_ID, 'type_id': typeId, 'str_id': strId})
        rows = dictfetchall(cursor)
        return rows

    def getById(self, typeId, strId):
        cursor = connection.cursor()
        cursor.execute(CStrTreeSQLGetStrId,
                       {'lng_id': settings.CDS_LNG_ID, 'type_id': typeId, 'str_id': strId})
        rows = dictfetchall(cursor)
        return rows[0]


class CSparesItemsManager(models.Manager):
    def list(self, typ_id, str_id):
        return CSpareItem.objects.raw(
            CSparesListByStrSQL,
            {'lng_id': settings.CDS_LNG_ID, 'typ_id': typ_id, 'str_id': str_id})

    def getById(self, article):
        cursor = connection.cursor()
        cursor.execute(CSparesListByArtSQL,
                       {'lng_id': settings.CDS_LNG_ID, 'article': article})
        rows = dictfetchall(cursor)
        return  CSpareItem(**rows[0])

    def criteries(self, art_id):
        cursor = connection.cursor()
        cursor.execute(CSparesCriteriaSQL,
                       {'lng_id': settings.CDS_LNG_ID, 'art_id': art_id})
        rows = dictfetchall(cursor)
        return rows

    def images(self, art_id):
        cursor = connection.cursor()
        cursor.execute(CSparesImagesSQL,
                       {'lng_id': settings.CDS_LNG_ID, 'art_id': art_id})
        rows = dictfetchall(cursor)
        return rows

    def applicables(self, art_id):
        return CCarVariants.objects.raw(CSparesApplicablesSQL,
                                        {'lng_id': settings.CDS_LNG_ID, 'art_id': art_id, 'brand': 'BMW'})


class CSpares(models.Model):
    carModels = CSparesCarModelsManager()
    carVariants = CSparesCarVariantsManager()
    strTree = CSparesStrTreeManager()
    items = CSparesItemsManager()

    class Meta:
        managed = False


class CCarModels(models.Model):
    name = models.CharField()
    brand = models.CharField()
    startMan = models.CharField()
    endMan = models.CharField()

    def _get_start_man(self):
        """Returns the start date of manufacturing"""
        year = self.startMan.__str__()[:4]
        month = self.startMan.__str__()[4:]
        return u'%s/%s' % (month, year)

    start_man = property(_get_start_man)

    def _get_end_man(self):
        """Returns the start date of manufacturing"""
        if self.endMan:
            year = self.endMan.__str__()[:4]
            month = self.endMan.__str__()[4:]
            return u'%s/%s' % (month, year)
        else:
            return ''

    end_man = property(_get_end_man)

    def _get_url(self):
        """Returns prepared url"""
        rname = self.name.replace(' ', '_')
        # if re.search('[F|E]([0-9]{1,2})', rname):
        #     rname = rname[rname.find('(') + 1:rname.find(')')].replace(',', '').replace(' ', '_')
        # else:
        #     rname = self.id
        #name_replace = rname.replace(u'кабрио', '').replace(u'купе', '').strip().replace(' ', '_').replace(',', '')
        return u'/spares/%s/' % rname

    url = property(_get_url)

    class Meta:
        managed = False


class CCarVariants(models.Model):
    name = models.CharField()
    modelId = models.IntegerField()
    startMan = models.CharField()
    endMan = models.CharField()
    hp = models.CharField()
    body = models.CharField()
    volume = models.CharField()
    kw = models.CharField()
    fuel = models.CharField()
    engine = models.CharField()
    cylinders = models.CharField()
    litres = models.CharField()
    valves = models.CharField()
    engineCode = models.CharField()
    fuelSupply = models.CharField()
    drive = models.CharField()
    weight = models.CharField()
    modelName = models.CharField()

    def _get_man_dates(self):
        startYear = self.startMan.__str__()[:4]
        startMonth = self.startMan.__str__()[4:]
        if self.endMan:
            stopYear = self.endMan.__str__()[:4]
            stopMonth = self.endMan.__str__()[4:]
            return u'%s/%s - %s/%s' % (startMonth, startYear, stopMonth, stopYear)
        else:
            return u'%s/%s - наст. время' % (startMonth, startYear)

    man_dates = property(_get_man_dates)

    def _get_model_name(self):
        return self.modelName.replace(' ', '_')

    model_name_url = property(_get_model_name)

    class Meta:
        managed = False


class CSpareItem(models.Model):
    name = models.CharField(max_length=255)
    supBrand = models.CharField(max_length=255)
    article = models.CharField(max_length=255)

    def _get_url(self):
        return u'/spares/article/%s/' % self.article.replace(' ', '_')

    url = property(_get_url)

    class Meta:
        managed = False